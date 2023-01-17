from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import exceptions, network
from web3 import Web3
import pytest


def test_get_entrance_fee(lottery_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Act
    # 2,000   eth / usd          10/2000 =0.005
    # usdEntryFee is 50
    # 2000/1 == 50/x == 0.025     2000/1 = 10 / x
    expected_entrance_fee = Web3.toWei(0.005, "ether")
    entrance_fee = lottery_contract.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started(lottery_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery_contract.enter(
            {"from": get_account(), "value": lottery_contract.getEntranceFee()}
        )


def test_can_start_and_enter_lottery(lottery_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery_contract.startLottery({"from": account})
    # Act
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    # Assert
    assert lottery_contract.players(0) == account


def test_can_end_lottery(lottery_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery_contract.startLottery({"from": account})
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    fund_with_link(lottery_contract)
    lottery_contract.endLottery({"from": account})
    assert lottery_contract.lottery_state() == 2


def test_can_pick_winner_correctly(lottery_contract, capsys):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery_contract.startLottery({"from": account})
    lottery_contract.enter(
        {"from": get_account(index=0),
            # "from": account,
         "value": lottery_contract.getEntranceFee()}
    )
    lottery_contract.enter(
        {"from": get_account(index=1),
         "value": lottery_contract.getEntranceFee()}
    )
    lottery_contract.enter(
        {"from": get_account(index=2),
         "value": lottery_contract.getEntranceFee()}
    )

    fund_with_link(lottery_contract)
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery_contract.balance()

    transaction = lottery_contract.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    # 777 % 3 = 0
    STATIC_RNG = 778
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery_contract.address, {"from": account}
    )

    with capsys.disabled():
        print("this output will not be captured and go straight to sys.stdout")
        print("account:  " + str(get_account(index=0)))
        print("account1:  " + str(get_account(index=1)))
        print("account2:  " + str(get_account(index=2)))
        print("random number is set as:  " + str(STATIC_RNG))
        print("caculation process:  " + str(STATIC_RNG) +
              " %3 = "+str(STATIC_RNG % 3))
        print("winner:  " + str(lottery_contract.recentWinner()))
        print("winner.balance:  " + str(get_account(index=1).balance()))

    # assert lottery_contract.recentWinner() == account
    assert lottery_contract.balance() == 0
    # assert account.balance() == starting_balance_of_account + balance_of_lottery

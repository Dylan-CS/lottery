1. Users can enter lottery with ETH BASED ON A USD FEE
2. AN ADMIN WILL CHOOSE WHEN THE LOTTERY IS OVRE
3. THE LOTTERY WILL SELECTA RANDOM WINNER 

How do we want to test this?
1. 'mainet-fork'
2. 'development with mocks'
3. 'testnet'

1.13 
The Smart Contract can't get the winner of the lottery, still need testing and modifying.

1.15 
1. local environment  check_test_lottery_unit and make it successful
2. network georli     check test_lottery_intergration.py ,still unsuccessful
3. local environment  try to deploy it ,get "0x0000000000000000000000000000000000000000 is the new winner!"
4. The two possible reasons may be the gas limit and the timesleep()

1.16 
1. local environment  test ,work successfully
2. local environment  try to deploy it in local environment.  Unsuccessful
3. get 10 LINK  Link币是运行于ChainLink系统的原生代币，供应总量10亿枚。
4. ChainLink是区块链中间件，它允许智能合同访问关键的离线资源，如数据提要、各种web API和传统的银行帐户支付。通过提供智能合同，确保对这些关键资源的访问，链环允许他们模拟真实的世界协议，这些协议需要外部的性能证明，并且需要支付广泛可用的支付方式，例如银行支付。换言之，与数据有关的行业，Chainlink都可以与之结合，所以有网友给Chainlink起了个外号“万能插头”。

 

        
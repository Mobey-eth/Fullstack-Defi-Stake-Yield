pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MockWETH is ERC20 {
    // This is our reward token which we give out to people who stake on our staking contract
    constructor() ERC20("Mock WETH", "wETH") {}
}

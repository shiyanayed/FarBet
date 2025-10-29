import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await ethers.provider.getBalance(deployer.address)).toString());
  
  // Set your Farcaster wallet address here
  const FEE_COLLECTOR_ADDRESS = process.env.FEE_COLLECTOR_ADDRESS || deployer.address;
  
  console.log("Fee collector address:", FEE_COLLECTOR_ADDRESS);
  
  const PredictionMarket = await ethers.getContractFactory("PredictionMarket");
  const predictionMarket = await PredictionMarket.deploy(FEE_COLLECTOR_ADDRESS);
  
  await predictionMarket.waitForDeployment();
  
  const address = await predictionMarket.getAddress();
  console.log("PredictionMarket deployed to:", address);
  
  // Save deployment info
  console.log("\nDeployment Summary:");
  console.log("===================");
  console.log("Network:", (await ethers.provider.getNetwork()).name);
  console.log("Contract Address:", address);
  console.log("Fee Collector:", FEE_COLLECTOR_ADDRESS);
  console.log("\nAdd this to your .env file:");
  console.log(`NEXT_PUBLIC_CONTRACT_ADDRESS=${address}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

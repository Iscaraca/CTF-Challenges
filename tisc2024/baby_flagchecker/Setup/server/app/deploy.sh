# Deploy contracts to anvil testnet
cd /contracts
/root/.foundry/bin/forge script script/Deploy.s.sol:Deploy --rpc-url http://testnet:8545 --json --broadcast --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 | tee /output.log
cd /app
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:5000
const { EtherscanProvider } = require('ethers');
const { Contract } = require('sevm');
require('sevm/4bytedb');

const bytecode = "0x5f3560e01c8063937c6c4414610013575f5ffd5b60043560243563d1efd30d60205260205f6004603c855af460205ff3";

const contract = new Contract(bytecode).patchdb(); // Lookup for 4byte matches
console.log(contract.solidify()); //Decompile bytecode to Solidity

const opcodes = contract.opcodes();
console.log(opcodes.map(opcode => opcode.format()));
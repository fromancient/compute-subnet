from typing import Optional
import pathlib

import bittensor
import argparse
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()
    PROJECT_NAME: str = "compute-subnet-miner"

    BITTENSOR_WALLET_DIRECTORY: pathlib.Path = Field(
        env="BITTENSOR_WALLET_DIRECTORY",
        default=pathlib.Path("~").expanduser() / ".bittensor" / "wallets",
    )
    BITTENSOR_WALLET_NAME: str = Field(env="BITTENSOR_WALLET_NAME")
    BITTENSOR_WALLET_HOTKEY_NAME: str = Field(env="BITTENSOR_WALLET_HOTKEY_NAME")
    BITTENSOR_NETUID: int = Field(env="BITTENSOR_NETUID")
    BITTENSOR_CHAIN_ENDPOINT: Optional[str] = Field(env="BITTENSOR_CHAIN_ENDPOINT", default=None)
    BITTENSOR_NETWORK: str = Field(env="BITTENSOR_NETWORK")

    SQLALCHEMY_DATABASE_URI: str = Field(env="SQLALCHEMY_DATABASE_URI")
    
    IP_ADDRESS: str = Field(env="IP_ADDRESS")
    PORT: int = Field(env="PORT", default=8000)

    class Config:
        env_file = ".env"

    def get_bittensor_wallet(self) -> bittensor.wallet:
        if not self.BITTENSOR_WALLET_NAME or not self.BITTENSOR_WALLET_HOTKEY_NAME:
            raise RuntimeError("Wallet not configured")
        wallet = bittensor.wallet(
            name=self.BITTENSOR_WALLET_NAME,
            hotkey=self.BITTENSOR_WALLET_HOTKEY_NAME,
            path=str(self.BITTENSOR_WALLET_DIRECTORY),
        )
        wallet.hotkey_file.get_keypair()  # this raises errors if the keys are inaccessible
        return wallet
    
    def get_bittensor_config(self) -> bittensor.config:
        parser = argparse.ArgumentParser()
        # bittensor.wallet.add_args(parser)
        # bittensor.subtensor.add_args(parser)
        # bittensor.logging.add_args(parser)
        # bittensor.axon.add_args(parser)
        
        if self.BITTENSOR_NETWORK:
            if '--subtensor.network' in parser._option_string_actions:
                parser._handle_conflict_resolve(None, [('--subtensor.network', parser._option_string_actions['--subtensor.network'])])

            parser.add_argument(
                "--subtensor.network",
                type=str,
                help="network",
                default=self.BITTENSOR_NETWORK,
            )
            
        if self.BITTENSOR_CHAIN_ENDPOINT:
            if '--subtensor.chain_endpoint' in parser._option_string_actions:
                parser._handle_conflict_resolve(None, [('--subtensor.chain_endpoint', parser._option_string_actions['--subtensor.chain_endpoint'])])

            parser.add_argument(
                "--subtensor.chain_endpoint",
                type=str,
                help="chain endpoint",
                default=self.BITTENSOR_CHAIN_ENDPOINT,
            )
            
        return bittensor.config(parser)
        

settings = Settings()

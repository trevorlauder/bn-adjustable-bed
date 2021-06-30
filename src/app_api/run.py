import uvicorn  # type: ignore

from api import Api
from config import get_config
from datastore import DataStore


def main():
    config = get_config()

    datastore = DataStore()

    api = Api(config=config, datastore=datastore)

    uvicorn.run(api, host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()

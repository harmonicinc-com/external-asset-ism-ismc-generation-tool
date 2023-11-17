# ISM/ISMC manifests generation

harmonic_external_asset_ism_ismc_generation_tool is a command line tool to generate the ISM/ISMC manifest for the .mp4 files stored in Azure containers.
The tool parses .mp4 files from an Azure container, generates .ism and .ismc manifests if they do not exist, and loads them into the Azure container. 

## Prerequisites
- Python 3.10
- Python libs:
  - azure-core==1.29.4
  - azure-storage-blob==12.8.1
  - azure-identity==1.14.1
  - pymp4==1.4.0
  - pycountry==22.3.5

## Supported codecs
### Video codecs
- AVC
- HEVC
### Audio codecs
- AAC-LC
- AAC-HE
- AAC+

## Supported formats:
- *.mp4 with single moov atom, without moof atoms

## HowTo run
```
python3 main.py -connection_string=<Azure storage account's connection string> -container_name=<Azure container name>
```
or
```
python3 main.py
```
in case if the configuration file azure_config.json has been filled (the configuration file shall be situated in the same folder as the main.py file).
### azure_config.json
azure_config.json - configuration file may contain the following fields: connection_string, account_name, account_key, container_name:
```
{
  "connection_string": "DefaultEndpointsProtocol=https;AccountName=flametestextassetstorage;AccountKey=<key>;EndpointSuffix=core.windows.net",
  "account_name": "flametestextassetstorage",
  "account_key": "<key>",
  "container_name": "test2"
}
```
It's possible to set the `connection_string`  fileld or `account_name` and `account_key` .
If only the `account_name` and `account_key` fields are specified, the connection string is formed from them.
If all fields are set, only the `connection_string` field value is used. In this case the `account_name` and `account_key` fields are ignored.

Azure connection string can be found in Azure Portal → Storage container → Access keys → Connection string


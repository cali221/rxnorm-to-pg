import pathlib
import requests
import dload
from datetime import datetime

# custom exception for unexpected API response
class UnexpectedResponseError(Exception):
    pass

def download_and_unzip(url, dest_dir):
    """
    download and unzip a folder from an URL into a destination path
    """
    returned_extract_path = dload.save_unzip(url, dest_dir)
    return returned_extract_path

def download_current_prescribable_content(monthlyOrWeekly):
    """
    download current prescribable content (monthly or weekly)
    """
    if monthlyOrWeekly == 'monthly':
        download_endpoint_url = 'https://uts-ws.nlm.nih.gov/releases?releaseType=rxnorm-prescribable-content-monthly-release&current=true'
    elif monthlyOrWeekly == 'weekly':
        download_endpoint_url = 'https://uts-ws.nlm.nih.gov/releases?releaseType=rxnorm-prescribable-content-weekly-updates&current=true'
    else:
        raise ValueError("Can only download weekly or monthly prescribable content")
    
    try:
        res_json = requests.get(download_endpoint_url).json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch RxNorm release information from API endpoint: {e}")

    # expect to get only one result for data for current prescribable content
    if len(res_json) == 1:
        # get download URL
        latest_download_url = res_json[0]['downloadUrl']
        print(f'Download URL: {latest_download_url}')

        # destination directory for the downloaded folder
        dest_dir = str(pathlib.Path(__file__).parent.parent.resolve() / 'downloaded_rxn_files' / f"{monthlyOrWeekly}_presc_content_downloaded_at_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")
        
        # download, unzip and return the path of the downloaded files
        try:
            print("Downloading and unzipping the folder....")
            downloaded_to = download_and_unzip(latest_download_url, dest_dir)
            print(f"Finished donwloading and unzipping the folder to {downloaded_to}")
        except Exception as e:
            raise RuntimeError(f"Failed to download and unzip the folder: {e}")

        return downloaded_to
    else:
        raise UnexpectedResponseError('Did not get 1 result, expected 1 result for current prescribable content')

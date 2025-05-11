import requests


class YaDriveAPI:
    def __init__(self, token):
        self._base_url = 'https://cloud-api.yandex.net/v1/disk/'
        self._headers = {            
            'Authorization': 'OAuth ' + token
        }

    def create_folder(self, folder_path):
        response = requests.put(self._base_url + 'resources',
                                params=self._params(folder_path),
                                headers=self._headers)
        return response.json()

    def direct_upload_file(self, file_link, file_path):
        response = requests.post(self._base_url + 'resources/upload',
                                 params=self._params(file_path, file_link),
                                 headers=self._headers)
        return response.json()
    
    def drive_info(self, get_code=False):
        response = requests.get(self._base_url,
                                headers=self._headers)
        if get_code:
            return response.status_code
        return response.text
    
    def FF_info(self, path, get_code=False):
        '''
        Get info about File of Folder
        '''
        response = requests.get(self._base_url + 'resources',
                                params=self._params(path),
                                headers=self._headers)
        if get_code:
            return response.status_code
        return response.text
    
    def operation_status(self, operation_id, get_code=False):
        response = requests.get(operation_id,
                                headers=self._headers)
        if get_code:
            return response.status_code
        return response.json()
    
    def _params(self, path, url=None):
        param = {
            'path': path,
            'overwrite': 'false',
            'url': url
        }
        return param

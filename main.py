from time import sleep
from modules.YaDriveAPI import YaDriveAPI
from modules.DogAPI import DogAPI
from modules.basic_functions import read_json_file, save_json_file
from modules.interact import ask, show_screen


def run_program():
    config = read_json_file('data/config.json')
    main_folder = 'RecopDogs'

    # If there's no token saved,
    # ask for one, check if valid and save it
    while not config['token']:
        config['token'] = set_token_dialog()
        save_json_file('data/config.json', config)

    YaDrive = YaDriveAPI(config['token'])

    # Load the breeds to check the input later
    show_screen('  loading all breeds...')
    all_breeds = DogAPI().get_all_breeds()['message']
    folders_checked = []

    while True:
        show_screen(' "Q" - close program\n'
                    ' "C" - change token\n\n' 
                    ' Please enter a breed or a command:',
                    smooth_in=True)

        choose = ask(' > ', lower=True)
        
        # Exit program
        if choose == 'q':
            break

        # Change token
        elif choose == 'c':
            config['token'] = set_token_dialog()
            save_json_file('data/config.json', config)

            YaDrive = YaDriveAPI(config['token'])

        # Check the breed, the folders needed
        # and upload the photo(s)
        else:
            # CHECK if the breed exists
            if choose not in all_breeds:
                show_screen('\n\n\n\n  >>> Invalid breed\n')
                sleep(1.5)
                continue

            # CHECK for subbreeds
            subbreeds = all_breeds.get(choose)
            if subbreeds:
                request = [[choose, subbreed] for subbreed in subbreeds]
            else:
                request = [[choose]]
            
            # CHECK if the program folder exists
            if main_folder not in folders_checked:
                show_screen(f'  checking for {main_folder} folder...')
                if YaDrive.FF_info(main_folder, get_code=True) == 404:
                    show_screen(f'  creating {main_folder} folder...\n')
                    YaDrive.create_folder(main_folder)
                folders_checked.append(main_folder)
            
            # CHECK if the breed folder exists
            if choose not in folders_checked:
                show_screen('  checking for '
                            f'{main_folder}/{choose} folder...')
                if YaDrive.FF_info(f'{main_folder}/{choose}',
                                    get_code=True) == 404:
                    show_screen('  creating '
                                f'{main_folder}/{choose} folder...\n')
                    YaDrive.create_folder(f'{main_folder}/{choose}')
                folders_checked.append(choose)

            # UPLOAD the photos
            upload_count = 0
            for breed in request:
                # Get photo link + its name
                show_screen(f'  getting {' '.join(breed)} photo link...')
                photos_links = DogAPI().get_breed_image(
                    '/'.join(breed))['message']

                # check for not uploaded photo
                for photo_link in photos_links:
                    photo_name = (f'{'_'.join(breed)}_'
                                  f'{photo_link.split("/")[-1]}')
                    if breed_saved(photo_name):
                        photo_name = None
                        continue
                    else:
                        break

                # if all photos are uploaded, skip
                if not photo_name:
                    show_screen(f'  >>> all {" ".join(breed)} '
                                 'photos already uploaded!\n')
                    sleep(2)
                    continue
                
                # Upload to Yandex Drive
                show_screen(f'   uploading {' '.join(breed)} photo...')
                operation = YaDrive.direct_upload_file(
                    photo_link,
                    f'{main_folder}/{choose}/{photo_name}')
                
                # wait for every photo to be uploaded (or not)
                while True:
                    status = YaDrive.operation_status(
                        operation['href'])['status']
                    if status == 'success':
                        upload_count += 1
                        update_uploaded_list(photo_name)
                        break
                    elif status == 'failed':
                        break

            show_screen(f'  >>> {upload_count} of {len(request)}'
                         ' photo(s) uploaded')
            sleep(3.5)
            

def set_token_dialog():
    '''
    Get token from user, accept only valid one
    '''
    while True:
        show_screen('  Please enter a valid token:')
        token = ask(' > ')
        if not token:
            continue

        show_screen('  checking token...')
        YaDrive = YaDriveAPI(token)
        if YaDrive.drive_info(get_code=True) == 401:
            show_screen('  >>> Token is invalid\n')
            token = None
            sleep(1.5)
            continue
        break

    return token


def breed_saved(photo_name):
    '''
    Check if the breed's photos are already uploaded
    '''
    uploaded = read_uploaded()
    for info in uploaded:
        if info['file_name'] == photo_name:
            return True

    return False


def update_uploaded_list(hoto_name):
    '''
    Update uploaded.json file with new photo's
    file name
    '''
    uploaded = read_uploaded()
    info = {
        'file_name': hoto_name
    }
    uploaded.append(info)
    save_json_file('data/uploaded.json', uploaded)


def read_uploaded():
    return read_json_file('data/uploaded.json')


if __name__ == '__main__':
    run_program()
# Sentinel 2 Data Fetcher

## Installation

- Create a Virtual Environment and activate it.
    
    ```shell
    python3 -m venv venv
    . venv/bin/activate
    ```

- Install the Package via pip.

    ```shell
    pip install sat-mapping-cyborg-ai
    ```
  
## Usage

- Import the Library

    ```python
    from sat_mapping import FolderData, folders_time_frame, Paths, download
    ```
  
- Set the Path to where you want to store the Satellite Data.

    ```python
    paths = Paths("<ANY/VALID/PATH>")
  
    ```

- Start the Download. (Note: One year needs around 110 GB Disk Space.)    

    ```python 
    download(paths, years=[2019], tiles=["32TMT"], months=[7])
    ```
  
- Load a folder.

    ```python
    folder_name = paths.folders[0]
    upper_left = (100000.0, 0.0)       # Postion on tile in [m]
    lower_right = (109800.0, 10000.0)  # Postion on tile in [m]
    data = FolderData(join(paths.data_path, folder_name), upper_left, lower_right)
    ```
  
- Display the image. (if matplotlib is not installed use <code>pip install matplotlib</code>)

    ```python
    import matplotlib.pyplot as plt
  
    picture = data.data[:, :, [3, 1, 2]]  # NIR, GREEN, BLUE
    fig: plt.Figure = plt.figure()
    plt.imshow(picture)
    plt.show()
    ```

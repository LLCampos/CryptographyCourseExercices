from Crypto.Hash import SHA256


def split_every_n_chars(string, n):
    return [string[i: i + n] for i in range(0, len(string), n)]


def get_h0_hash(video_file_path):
    with open(video_file_path, 'rb') as f:
        binary_video_data = f.read()

    # Split every 1 kb
    blocks = split_every_n_chars(binary_video_data, 1024)
    blocks.reverse()

    for i, block in enumerate(blocks):
        sha = SHA256.new(block)
        if i + 1 == len(blocks):
            print sha.hexdigest()
        else:
            blocks[i + 1] += sha.digest()

if __name__ == '__main__':
    video_file_path = '6.2.birthday.mp4_download'
    get_h0_hash(video_file_path)

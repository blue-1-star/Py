import subprocess

def get_video_creation_date(video_path):
    try:
        result = subprocess.run(
            ['G:/Soft/PORTABLE/exiftool', '-CreateDate', '-d', '%Y-%m-%d %H:%M:%S', video_path],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output:
            # exiftool возвращает строку вида "Create Date : 2023-05-27 13:34:45"
            creation_date = output.split(':', 1)[1].strip()
            return creation_date
        else:
            return "Дата создания не найдена"
    except Exception as e:
        return str(e)

video_path1 = 'g:/test/VID_20230527_133445.mp4'
video_path2 = 'g:/test/VID_20240528_160201.mp4'
video_path3 = 'G:/Photo/OnePlus/Video/VID_20220719_115940.mp4'
l = []
l = get_video_creation_date(video_path1), get_video_creation_date(video_path2), get_video_creation_date(video_path3)
print(f'Дата создания видеофайла: {l}')

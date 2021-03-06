from World import World
from Reconstruct import Camera
from utils.path_parser import get_camera_info_dir
from utils.openpose import json_pack
import argparse
import os
from ActionAnylsis.Action import Action
import json

Asset_path = 'asset'


def main():
    parser = argparse.ArgumentParser(
        description='Reconstruct and Analysis for volleyball training')

    parser.add_argument('--camera0-name', '-c0n', type=str, default='cam0')
    parser.add_argument('--camera1-name', '-c1n', type=str, default='cam1')
    parser.add_argument('--c0-video-dir', '-v0', type=str, default=os.path.join(Asset_path, 'videos/v0c0.mp4'))
    parser.add_argument('--c1-video-dir', '-v1', type=str, default=os.path.join(Asset_path, 'videos/v0c1.mp4'))

    parser.add_argument('--c0-cali-video', '-c0-cali', type=str, default=None)
    parser.add_argument('--c1-cali-video', '-c1-cali', type=str, default=None)

    parser.add_argument('--land-marker', '-lm', type=str, default=None)

    parser.add_argument('--openpose-build', '-op', type=str,
                        default="/home/fyq/openpose/build/examples/openpose/openpose.bin")

    parser.add_argument('--openpose_work_path', '-owp', type=str,
                        default=os.path.join(Asset_path, 'openpose_data'))

    parser.add_argument('--ball-work-path', '-bwp', type=str,
                        default=os.path.join(Asset_path, 'ball'))

    parser.add_argument('--label_name_dir', type=str, default='st_gcn/resource/**.txt')

    parser.add_argument('--fps', '-f', type=float, default=60.)
    parser.add_argument('--gpu', '-g', type=int, default=0)
    parser.add_argument('--lr', '-l', type=float, default=1e-3)
    parser.add_argument('--out', '-o', default='result',
                        help='Output directory')
    args = parser.parse_args()

    cam0 = Camera(0, args.camera0_name, camera_matrix=None, calibration_video=args.c0_cali_video, land_marker=args.land_marker)
    cam1 = Camera(1, args.camera1_name, camera_matrix=None, calibration_video=args.c1_cali_video, land_marker=args.land_marker)

    cams = [cam0, cam1]

    video_dirs = [args.c0_video_dir, args.c1_video_dir]

    world = World(cams, video_dirs, args.openpose_work_path, args.ball_work_path, args.fps)
    world.detection_and_reconstruct()

    demo_action = Action(start_frame=0, end_frame=230, action_name='underhand_server')

    result = world.analyse_action(demo_action)
    world.save_demo_result(result)
    print(result)

    # now we are not really use action recognize module
    # action_json_dir = os.path.join(args.openpose_work__path, "actions.json")
    # video_dir = video_dirs[0]
    # video_name = video_dir[video_dir.rfind('/') + 1:].split('.')[0]
    # command_line = './st_gcn/st_gcn.py -vh 1080 -vw 1920 --video_name {} ' \
    #                '--openpose_work_path {} --label_name_dir {} --action_json_dir {}'.format(
    #                 video_name, args.openpose_work_path, args.label_name_dir, action_json_dir)
    # os.system(command_line)

    # action_sequence = json.load(open(action_json_dir, 'r'))['actions']

    # world.analyse(action_sequence)
    # world.show_result()



if __name__ == '__main__':
    main()

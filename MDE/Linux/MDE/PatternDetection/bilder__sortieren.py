import os
import cv2
from detect_pattern import ImageMatcher

def sort_images(input_dir):
    matcher = ImageMatcher()
    

    for input_filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, input_filename)
        img = cv2.imread(input_path)
        #print('input_path', input_path)
        pattern_id = matcher.match_images(img)


        if not os.path.exists(f"sorted_imgs/{pattern_id}"):
            os.makedirs(f"sorted_imgs/{pattern_id}")
            try:
              cv2.imwrite(f"sorted_imgs/{pattern_id}/template_merkamal.tiff", matcher.templates[pattern_id])
              pattern_img = cv2.imread(matcher.temp_id_path[pattern_id])
              cv2.imwrite(f"sorted_imgs/{pattern_id}/template.tiff", pattern_img)
            
            except:#wenn patten id = -1
                pass

            #print(f"sorted_imgs/{pattern_id}/template.tiff")

        cv2.imwrite(f"sorted_imgs/{pattern_id}/{input_filename}", img)


def main():
    input_dir = '/home/pi/Downloads/gildemeister/13-14Uhr'
    sort_images(input_dir)


if __name__ == '__main__':
    main()




import cv2
import aircv as ac

def draw_circle(img, pos, circle_radius, color, line_width):
	cv2.circle(img, pos, circle_radius, color, line_width)
	cv2.imshow('objDetect', imsrc)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == "__main__":
	imsrc = ac.imread('a.jpg')
	imobj = ac.imread('b.jpg')

	# find the match position
	pos = ac.find_template(imsrc, imobj)
	print(pos)
	circle_center_pos = list(pos['result'])
	x = int(circle_center_pos[0])
	y = int(circle_center_pos[1])
	position = (x,y)
	circle_radius = 5
	color = (0, 255, 0)
	line_width = 1

	# draw circle
	draw_circle(imsrc, position, circle_radius, color, line_width)

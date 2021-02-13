from PIL import Image
import numpy as np
import matplotlib.pyplot as mplot
import sys

def histogram_equalize(arr):
    shape = arr.shape
    size = shape[0] * shape[1]

    out = np.zeros(shape)
    #create an array to store the counts of each value
    c = []
    for i in range(256):
        c.append(0.0)

    #populate count array
    for i in range(shape[0]):
        for j in range(shape[1]):
            c[arr[i][j]] += 1
    
    #Transform to probability
    for i in range(256):
        c[i] /= size 
    
    #Cumulative
    for i in range(0,256):
        c[i] += c[i-1] 
    
    #Equalize
    for i in range(256):
        c[i] *= 255

    #Process image
    for i in range(shape[0]):
        for j in range(shape[1]):
            v = arr[i][j] #Get the color value
            val = int(c[v])
            out[i][j] = val #Set it's equalized value to new image

    #Return new image 
    return out


def create_histogram_plot(img, figname):
    shape = img.shape
     #create an array to store the counts of each value
    c = []
    for i in range(256):
        c.append(0)

    #populate count array
    
    for i in range(shape[0]):
        for j in range(shape[1]):
            c[img[i][j]] += 1
    
    for i in range(0,256):
        c[i] += c[i-1] 

    #Pixel values
    x = []
    for i in range(256):
        x.append(i)

    mplot.plot(x, c)
    mplot.savefig(figname)
    mplot.show()


def process_image(name):
    #Get input image
    input_img = Image.open(name).convert("L")
    #Save image as grayscale
    input_img.save("greyscale.bmp")

    #Convert image to array for processing
    a = np.asarray(input_img)
    #Process image
    out = histogram_equalize(a)
    #Convert processed array to image
    processed_img = Image.fromarray(out.astype('uint8'), 'L')

    #Create histograms and save them for the images
    create_histogram_plot(a, "input_graph")
    create_histogram_plot(np.asarray(processed_img), "output_graph")


    #Create the ouput image as grayscaled input and output side by side
    output = Image.new('L', (input_img.width * 2, input_img.height))
    output.paste(input_img, (0,0))
    output.paste(processed_img, (input_img.width, 0))
    output.show()
    output.save("output.bmp")


def main():
    if(len(sys.argv) == 2):
        process_image(sys.argv[1])
    else:
        process_image("test.bmp")

if __name__ == "__main__":
    main()

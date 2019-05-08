# coding:utf-8
# from pdf2image import convert_from_path
# import tempfile
#
#
# def main(filename, outputDir):
#     print('filename=', filename)
#     print('outputDir=', outputDir)
#     with tempfile.TemporaryDirectory() as path:
#         images = convert_from_path(filename)
#         for index, img in enumerate(images):
#             img.save('%s/page_%s.png' % (outputDir, index))
#
#
# if __name__ == "__main__":
#     main('../000PublicData/demo.pdf', '../000PublicData/image')

from wand.image import Image


def convert_pdf_to_jpg(filename):
    with Image(filename=filename) as img :
        print('pages = ', len(img.sequence))

        with img.convert('jpeg') as converted:
            converted.save(filename='image/page.jpeg')


convert_pdf_to_jpg('../000PublicData/demo.pdf')

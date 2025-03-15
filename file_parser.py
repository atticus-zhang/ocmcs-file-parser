import os
import time
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from dynamsoft_barcode_reader_bundle import *



def get_all_pages():
    folder_path = "./inPdf/"
    dpi = 150

    all_pages = []

    start_time = time.time()

    for file_name in os.listdir(folder_path):
        
        if file_name.endswith(".pdf") :
            pages = convert_from_path(folder_path + file_name, dpi = dpi, thread_count=8)
            all_pages.extend(pages)
        elif not file_name.startswith("."):
            page = Image.open(folder_path + file_name)
            all_pages.append(page)
    
    end_time = time.time()
    time_taken = end_time - start_time

    print(f'PDF to image:\n{len(all_pages)} pages converted at dpi {dpi}\n{time_taken:.2f} seconds taken\n\n')
    
    return all_pages

def convert_to_bgr(pil_images):

    start_time = time.time()

    np_array = []

    for i in range(len(pil_images)):
        img = np.array(pil_images[i])

        height = img.shape[0]

        top_quarter = img[:height // 5, :]

        top_quarter_bgr = top_quarter[..., ::-1]

        np_array.append(top_quarter_bgr)
        # np_array.append(np.array(pil_images[i]))
    
    end_time = time.time()
    time_taken = end_time - start_time

    print(f'PIL to np.array:\n{len(pil_images)} pages converted\n{time_taken:.2f} seconds taken\n\n')

    return np_array

def decode(nparray_pages):
    detection_failed = 0
    exams_scanned = 0
    page_sorted = {"no_barcode_detected": []}

    errorCode, errorMsg = LicenseManager.init_license("t0068lQAAAFOzmd4LuzieTZiIUJB0/zbVbun10frmeJpQglgX+5yRwXCYNHWoiRKMDkQca2pt1eyBAy2gFBJenqGlz3YtFSs=;t0069lQAAAGfEQ04ThQCnPBRkXD1c0coSrEPVKx9aOqX6/DXjXjiOn2aEn8WpF1mLMT68yR7TFTH3RaOzyu+2vWwipTEgbBNg;t0069lQAAAAaaOX6utHM4pTlZ7t0wGDRL1b1LRHdbYLNvacxR50R9pR2+3ocPFfJPLSv6yppCVuJoadTgopabM2/YugPMnQdg")
    if errorCode != EnumErrorCode.EC_OK and errorCode != EnumErrorCode.EC_LICENSE_CACHE_USED:
        print("License initialization failed: ErrorCode:", errorCode, ", ErrorString:", errorMsg)
    else:
        cvr = CaptureVisionRouter()
        start_time = time.time()
        for i in range(len(nparray_pages)):
            result = cvr.capture(nparray_pages[i])
            if result.get_error_code() != EnumErrorCode.EC_OK:
                print("Error:", result.get_error_code(), result.get_error_string())
            barcode_result = result.get_decoded_barcodes_result()
            if barcode_result is None or barcode_result.get_items() == 0:
                page_sorted["no_barcode_detected"].append(i)
                detection_failed += 1
            else:
                items = barcode_result.get_items()
                sn = items[0].get_text()
                if sn in page_sorted:
                    page_sorted[sn].append(i)
                else:
                    page_sorted[sn] = [i]
                    exams_scanned += 1
        end_time = time.time()
        time_taken = end_time - start_time
        print(f'Detecting barcodes:\n{len(nparray_pages)} pages scanned\n{time_taken:.2f} seconds taken\n')
        print(f'Exam scanned: {exams_scanned}\nDetection failed on {detection_failed} pages\n\n')
    return page_sorted


def save_to_desination(page_sorted, pil_images):
    folder_path = "./outPdf/"

    start_time = time.time()
    for document in page_sorted:
        doc_pages = []
        for page_number in page_sorted[document]:
            doc_pages.append(pil_images[page_number])

        doc_pages[0].save(
            f"{folder_path}/{document}.pdf",
            save_all=True,
            append_images=doc_pages[1:],
            optimize=True
        )
    end_time = time.time()
    time_taken = end_time - start_time
    print(f'Converting to PDF:\n{len(page_sorted)} documents converted\n{time_taken:.2f} seconds taken\n\n')


def main():
    print("Loading pages...")
    start_time = time.time()
    pil_pages = get_all_pages()
    np_array = convert_to_bgr(pil_pages)
    sorted_pages = decode(np_array)
    save_to_desination(sorted_pages, pil_pages)
    end_time = time.time()

    time_taken = end_time - start_time
    print(f'Scanning complete!\n{time_taken:.2f} seconds taken in total\n\n')

main()

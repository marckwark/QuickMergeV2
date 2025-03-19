import os
import re
import fitz  # Using PyMuPDF instead of PyPDF2
from datetime import datetime
from natsort import natsorted
import shutil

def copy_and_merge_pdfs(sequence, num_digits, input_folder, project_code,
                        output_folder, start_date, end_date, merged_pdf_name):
    if not os.path.isdir(input_folder):
        raise ValueError(f"The folder '{input_folder}' does not exist")
    
    regex_pattern = re.compile(rf'{re.escape(sequence)}(\d{{{num_digits}}})')
    pdf_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder)
                 if project_code in f and f.lower().endswith('.pdf')]
    
    pdf_files = natsorted(pdf_files, key=lambda x: regex_pattern.search(x).group(1) if regex_pattern.search(x) else '')
    
    # Convert start/end dates
    start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")
    end_date_obj = datetime.strptime(end_date, "%d-%m-%Y")
    end_date_obj = end_date_obj.replace(hour=23, minute=59, second=59)
    
    filtered_pdfs = []
    for pdf in pdf_files:
        try:
            doc = fitz.open(pdf)
            metadata = doc.metadata
            pdf_date_obj = None
            pdf_date_str = None
            if metadata.get("modDate"):
                pdf_date_str = metadata.get("modDate")
            elif metadata.get("creationDate"):
                pdf_date_str = metadata.get("creationDate")
            if pdf_date_str:
                if pdf_date_str.startswith("D:"):
                    pdf_date_str = pdf_date_str[2:]
                pdf_date_obj = datetime.strptime(pdf_date_str[:14], "%Y%m%d%H%M%S")
            if pdf_date_obj and start_date_obj <= pdf_date_obj <= end_date_obj:
                filtered_pdfs.append(pdf)
        except Exception as e:
            print(f"Error processing {pdf}: {e}")
    
    # Copy filtered PDFs to output folder using shutil.copy2
    for pdf in filtered_pdfs:
        destination = os.path.join(output_folder, os.path.basename(pdf))
        try:
            shutil.copy2(pdf, destination)
        except Exception as e:
            print(f"Failed to copy {pdf} to {destination}: {e}")
    
    # Merge them using PyMuPDF
    merged_pdf_path = os.path.join(output_folder, merged_pdf_name + ".pdf")
    merged_doc = fitz.open()
    try:
        for pdf in filtered_pdfs:
            try:
                doc = fitz.open(pdf)
                merged_doc.insert_pdf(doc)
                doc.close()
            except Exception as e:
                print(f"Error merging {pdf}: {e}")
        merged_doc.save(merged_pdf_path)
        print(f"Merged PDF saved to {merged_pdf_path}")
    except Exception as e:
        print(f"Failed to create merged PDF: {e}")
    finally:
        merged_doc.close()
    
    return filtered_pdfs, merged_pdf_path

def progressive_order_pdfs(file_list, substring, digits):
    """
    Orders a list of PDF file paths by extracting a numeric value from filenames.
    Files that do not contain the specified substring followed immediately by the exact number
    of digits are considered unmatched and are placed at the beginning of the final list.
    
    Parameters:
      file_list: List of PDF file paths.
      substring: The substring that should precede the numeric portion in the filename.
      digits: The exact number of digits following the substring.
    
    Returns:
      A list of file paths where unmatched files come first (preserving their original order),
      followed by the matched files sorted by the extracted numeric value.
    """
    pattern = re.compile(re.escape(substring) + r'(\d{' + str(digits) + r'})')
    matched_files = []
    unmatched_files = []
    
    for f in file_list:
        basename = os.path.basename(f)
        match = pattern.search(basename)
        if match:
            try:
                number = int(match.group(1))
                matched_files.append((f, number))
            except Exception:
                unmatched_files.append(f)
        else:
            unmatched_files.append(f)
    
    matched_files.sort(key=lambda x: x[1])
    ordered_files = unmatched_files + [mf[0] for mf in matched_files]
    return ordered_files

def merge_pdf_files(pdf_list, output_pdf_path):
    merged_doc = fitz.open()
    try:
        for pdf in pdf_list:
            try:
                doc = fitz.open(pdf)
                merged_doc.insert_pdf(doc)
                doc.close()
            except Exception as e:
                print(f"Error merging {pdf}: {e}")
        merged_doc.save(output_pdf_path)
    except Exception as e:
        raise RuntimeError(f"Failed to merge PDFs: {e}")
    finally:
        merged_doc.close()
    return output_pdf_path
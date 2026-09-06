import os
import rasterio


def detect_modality(image_path):

    """
    Detect image modality from folder/file name.
    """

    path = image_path.lower()

    if "optical" in path:
        return "optical"

    if "sar" in path:
        return "sar"

    return "unknown"



def validate_images(image_paths, intent):

    """
    Validate uploaded images based on intent.

    single_image:
        1 image

    bi_temporal:
        2 images (before/after)

    cross_modal:
        optical + SAR
    """


    if not image_paths:

        return {
            "valid": False,
            "message": "No images provided."
        }



    image_count = len(image_paths)


    modalities = []



    # Check images exist and read metadata

    for image in image_paths:


        if not os.path.exists(image):

            return {
                "valid": False,
                "message": f"Image not found: {image}"
            }


        try:

            with rasterio.open(image) as src:

                modality = detect_modality(image)

                modalities.append(modality)



        except Exception as e:

            return {
                "valid":False,
                "message":f"Invalid raster file: {e}"
            }



    # Remove duplicate values

    modalities = list(set(modalities))



    # -----------------------------
    # Single image validation
    # -----------------------------

    if intent == "single_image":


        if image_count != 1:

            return {

                "valid":False,

                "message":
                "single_image requires exactly one image."

            }



    # -----------------------------
    # Bi temporal validation
    # -----------------------------

    elif intent == "bi_temporal":


        if image_count != 2:

            return {

                "valid":False,

                "message":
                "bi_temporal requires two images."

            }



    # -----------------------------
    # Cross modal validation
    # -----------------------------

    elif intent == "cross_modal":


        if image_count != 2:


            return {

                "valid":False,

                "message":
                "cross_modal requires optical and SAR images."

            }



        if set(modalities) != {"optical","sar"}:


            return {

                "valid":False,

                "message":
                "Need one optical image and one SAR image."

            }



    else:


        return {

            "valid":False,

            "message":
            "Unknown intent."

        }



    return {

        "valid":True,

        "image_count":image_count,

        "modalities":modalities,

        "images":image_paths,

        "message":
        "Image validation successful."

    }
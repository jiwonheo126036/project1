package com.example.kiosk

import com.google.gson.annotations.SerializedName
import org.json.JSONArray
import org.json.JSONObject

data class ImageUrlData(
    @SerializedName("url_list") var url_list : List<String>,
)

data class PostImage(
    @SerializedName("kiosk_id") val kiosk_id : Int,
    @SerializedName("face_image") val face_image : String
)
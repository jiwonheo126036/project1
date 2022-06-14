package com.example.kiosk

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*

interface RetrofitService {
//    @FormUrlEncoded
    @POST("/post_image/")
    @Headers("accept: application/json","content-type:application/json")
    fun postImagePath(
        @Body PostImage: PostImage
    ): Call<ImageUrlData>

    @GET("/no_user/")
    fun getImagePath(): Call<ImageUrlData>

    companion object{
        private const val BASE_URL = "https://www.mclabha.com"

        fun create():RetrofitService{
        val gson: Gson = GsonBuilder().setLenient().create();

            return Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create(gson))
                .build()
                .create(RetrofitService::class.java)
                }
        }
}
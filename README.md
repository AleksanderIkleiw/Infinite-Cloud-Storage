
#Infinite Cloud Storage

The program allows users to deposit any file of their choosing on the free cloud(youtube). It is possible by byte converting into video and then lossless decoding. Hashes of files before hosting and after decoding are the same. After youtube's policy update, you have to manually host video produced by the program.


## Function Reference

#### Convert file to video

```http
  private_num = 8
   obj2 = CreateImages(filename, username, security_num)
   obj2.main()
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `filename` | `string` | Self explainatory|
| `username` | `string` | Username that will be used in the database(gateway for web version)|
|`security_num`| `integer`| Number to multiply every bit |

#### Convert video to file

```http
  obj = CreateFileFromVideo(filename, username, security_number, local=False)
  obj.main()
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | Self explainatory |
| `username`      | `string` | Username that will be used in the database(gateway for web version) |
| `security_number`| `string` | Number to multiply every bit |
| `local`      | `boolean` | **Optional** if True color values won't be converted to white/black |



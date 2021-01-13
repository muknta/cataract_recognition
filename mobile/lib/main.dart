import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Cataract detection'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var _image;
  var _result;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            _image != null
                ? ClipRRect(
                    borderRadius: BorderRadius.circular(50),
                    child: Image.file(
                      _image,
                      width: 200,
                      height: 200,
                      fit: BoxFit.fitHeight,
                    ),
                  )
                : Container(
                    decoration: BoxDecoration(
                        color: Colors.grey[200],
                        borderRadius: BorderRadius.circular(50)),
                    width: 200,
                    height: 200,
                  ),
            Text(
              'Select image for cataract detection',
            ),
            _result != null
                ? Text(
                    'Cataract probability: ${_result["cataract_probability"]}',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  )
                : Container(),
            Row(mainAxisAlignment: MainAxisAlignment.center, children: [
              IconButton(
                  color: Theme.of(context).accentColor,
                  icon: Icon(
                    Icons.photo_camera,
                  ),
                  iconSize: 50,
                  onPressed: () async => getImage(ImageSource.camera)
                      .then((value) => _upload(value))),
              IconButton(
                  icon: Icon(Icons.photo),
                  iconSize: 50,
                  color: Theme.of(context).accentColor,
                  onPressed: () async => getImage(ImageSource.gallery)
                      .then((value) => _upload(value))
                      .then((value) => null))
            ])
          ],
        ),
      ),
    );
  }

  Future getImage(ImageSource source) async {
    final picker = ImagePicker();

    final image = await picker.getImage(
        source: source,
        imageQuality: 50, // <- Reduce Image quality
        maxHeight: 500, // <- reduce the image size
        maxWidth: 500);
    setState(() {
      _image = File(image.path);
    });
    return image;
  }

  void _upload(file) async {
    String fileName = file.path.split('/').last;
    print('Got file with path: $fileName');
    FormData data = FormData.fromMap({
      "file": await MultipartFile.fromFile(
        file.path,
        filename: fileName,
      ),
    });

    Dio dio = new Dio();

    dio
        .post("http://35.225.157.197:8000/cataract/detect", data: data)
        .then((response) {
      Map data = response.data;
      if (data != null) {
        if (data["result"] == true) {
          setState(() {
            _result = data;
          });
        }
      }
    }).catchError((error) => print(error));
  }
}

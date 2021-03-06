
    // Rectangle {
    //     id: rect1
    //     anchors.fill: parent;

    //     Image {
    //         id: image0
    //         source: sessionData.rootPath + "/media/a/f735bee5b64ef98879dc618b016ecf7939a5756040c2cde21ccb15e69a6e1cfb.png"
    //         width: 1
    //         height: 1
    //     }        

    //     Image {
    //         id: image1
    //         source: sessionData.rootPath + "/media/a/52d2a8f514c4fd2d9866587f4d7b2a5bfa1a11a0e772077d7682deb8b3b517e5.jpg"
    //         width: 1
    //         height: 1
    //     }        

    //     ShaderEffect {
    //         id: shaderEffect
    //         anchors.fill: parent
    //         //width: parent.width / 2
    //         //height: parent.height / 2
    //         property variant startTime: Date.now() + 0;
    //         property variant iTime: (Date.now() - startTime) / 1000.0;
    //         property variant color: Qt.vector3d(0.344, 0.5, 0.156);
    //         property variant iResolution: Qt.vector3d(parent.width, parent.height, 1.0);
    //         property variant iDate: Qt.vector4d(0, 0, 0, 0);
    //         property variant iChannel0: image0
    //         property variant iChannel1: image1

    //         function update() {
    //             iTime = (Date.now() - startTime) / 1000.0;
    //             iDate.w = iTime;
    //         }

    //         fragmentShader: sessionData.shaderPath
    //         Component.onCompleted: startTime = startTime;
    //         Timer { interval: 15; running: visible; repeat: true; onTriggered: shaderEffect.update(); }
    //     }            

    //     // Grid {
    //     //     id: grid1
    //     //     anchors.fill: parent
    //     //     spacing: 2
    //     //     columns: width / 10
    //     //     property var cellCount: width * height / 100;
    //     //     Repeater {
    //     //         model: grid1.cellCount
    //     //         Rectangle {
    //     //             width: 8; height: 8;
    //     //             color: "cyan"
    //     //         }
    //     //     }
    //     // }
    // }
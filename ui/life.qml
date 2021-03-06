import QtQuick 2.8
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.4
import QtMultimedia 5.12
import QtQuick 2.2 as QQ2
import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.12
import QtQuick 2.0
import QtQuick.Scene3D 2.0
import org.kde.kirigami 2.4 as Kirigami
import Mycroft 1.0 as Mycroft


Mycroft.Delegate {
    id: root
    property var rootPath: sessionData.rootPath
    property var cellSize: sessionData.cellSize || 10

    // Component.onCompleted: {
    //     console.log("API: " + GraphicsInfo.api)
    //     console.log("Version: " + GraphicsInfo.majorVersion + "." + GraphicsInfo.minoeVersion)
    //     console.log("renderableType : " + GraphicsInfo.renderableType)
    // }

    onVisibleChanged: {
        if (!visible) {
            triggerGuiEvent("gameoflife.notvisible", {}) 
        }
    }

    function getCellCount(width, height, cellSize) {
        return (width * height) / (cellSize * cellSize)
    }

    GridView {
        id: grid
        anchors.fill: parent
        cellWidth: sessionData.cellSize
        cellHeight: sessionData.cellSize
        model: sessionData.model
        property bool init: false

        Component.onCompleted: console.log("Grid view is up")

        onWidthChanged: sizeUpdated()
        onHeightChanged: sizeUpdated()

        function sizeUpdated() {
            console.log("Size updated")
            if (width !== 0 && height !== 0 && !init) {
                console.log("Sending grid complete")
                triggerGuiEvent("gameoflife.gridComplete", { "width": width, "height": height });
                init = true;
            }
        }

        delegate: Rectangle {
            color: age > 0 ? "red" : "blue"
            width: grid.cellWidth; height: grid.cellHeight
        }
    }
}

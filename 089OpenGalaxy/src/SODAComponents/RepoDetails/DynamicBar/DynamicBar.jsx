import React from "react";
import * as ANI from "anichart";
import { format } from "d3";
import PlayButton from "./PlayButton/PlayButton.jsx";

class DynamicBar extends React.Component {
  constructor() {
    super();
    this.previousUrl = null;
    this.stage = null;
    this.timer = null;

    this.play = this.play.bind(this);
    this.setPlaying = this.setPlaying.bind(this);

    this.state = {
      playing: false,
    };
  }

  play() {
    this.stage.interval = null;
    this.stage.sec = 0;
    this.stage.play();
    this.setPlaying(true);
    this.timer = setTimeout(() => {
      this.setPlaying(false);
    }, (this.props.duration + 1) * 1000);
  }

  setPlaying(isPlaying) {
    this.setState({
      playing: isPlaying,
    });
  }

  componentDidMount() {
    this.previousUrl = this.props.dataUrl;

    let idSet = new Set();
    ANI.recourse.loadCSV(this.props.dataUrl, "data").then(() => {
      ANI.recourse.setup().then(() => {
        ANI.recourse.data.get("data").forEach((item) => idSet.add(item.id));
        idSet.forEach((username) => {
          ANI.recourse.loadImage(
            `https://avatars.githubusercontent.com/${username}?s=128&v=4`,
            username
          );
        });
      });
    });

    this.stage = new ANI.Stage(document.getElementById("dynamic-bar"));
    this.stage.options.fps = 30;
    this.stage.options.sec = this.props.duration;
    this.stage.output = false;

    const barChart = new ANI.BarChart({
      dataName: "data",
      idField: "id",
      showDateLabel: true,
      itemCount: this.props.barNumber,
      aniTime: [0, this.props.duration],
      swapDurationMS: 300,
      showRankLabel: false,
      margin: { left: 20, right: 20, top: 20, bottom: 20 },
      dateLabelOptions: {
        fontSize: this.props.dateLabelSize,
        fillStyle: "#777",
        textAlign: "right",
        fontWeight: "bolder",
        textBaseline: "alphabetic",
        position: {
          x: this.stage.canvas.width - 20,
          y: this.stage.canvas.height - 20,
        },
      },
      valueFormat: (cData) => {
        return format(`,.${this.props.digitNumber}f`)(cData["value"]);
      },
    });

    this.stage.addChild(barChart);

    this.stage.render(this.props.duration);
  }

  componentDidUpdate() {
    // 如果结点切换了, 那么组件的状态和数据都要刷新
    if (this.props.dataUrl != this.previousUrl) {
      this.previousUrl = this.props.dataUrl;

      if (this.timer) {
        clearTimeout(this.timer);
        this.timer = null;
      }

      if (this.stage.playing) {
        this.stage.play(); // play() is a toggle method, here means stop.
        this.setPlaying(false);
      }
      this.stage = null;

      let idSet = new Set();
      ANI.recourse.loadCSV(this.props.dataUrl, "data").then(() => {
        ANI.recourse.setup().then(() => {
          ANI.recourse.data.get("data").forEach((item) => idSet.add(item.id));
          idSet.forEach((username) => {
            ANI.recourse.loadImage(
              `https://avatars.githubusercontent.com/${username}?s=128&v=4`,
              username
            );
          });
        });
      });

      this.stage = new ANI.Stage(document.getElementById("dynamic-bar"));
      this.stage.options.fps = 30;
      this.stage.options.sec = this.props.duration;
      this.stage.output = false;

      const barChart = new ANI.BarChart({
        dataName: "data",
        idField: "id",
        showDateLabel: true,
        itemCount: this.props.barNumber,
        aniTime: [0, this.props.duration],
        swapDurationMS: 300,
        showRankLabel: false,
        margin: { left: 20, right: 20, top: 20, bottom: 20 },
        dateLabelOptions: {
          fontSize: this.props.dateLabelSize,
          fillStyle: "#777",
          textAlign: "right",
          fontWeight: "bolder",
          textBaseline: "alphabetic",
          position: {
            x: this.stage.canvas.width - 20,
            y: this.stage.canvas.height - 20,
          },
        },
        valueFormat: (cData) => {
          return format(`,.${this.props.digitNumber}f`)(cData["value"]);
        },
      });

      this.stage.addChild(barChart);

      this.stage.render(this.props.duration);
    }
  }

  render() {
    return (
      <div style={{ position: "relative" }}>
        <canvas
          id="dynamic-bar"
          width={this.props.width}
          height={this.props.height}
        />
        <PlayButton
          hide={this.state.playing}
          theme={this.props.theme}
          play={this.play}
        />
      </div>
    );
  }
}

export default DynamicBar;

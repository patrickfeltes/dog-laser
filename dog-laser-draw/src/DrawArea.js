import Immutable from "immutable";
import React from 'react';

class DrawArea extends React.Component {
    constructor() {
      super();
  
      this.state = {
        lines: new Immutable.List(),
        isDrawing: false
      };
  
      this.handleMouseDown = this.handleMouseDown.bind(this);
      this.handleMouseMove = this.handleMouseMove.bind(this);
      this.handleMouseUp = this.handleMouseUp.bind(this);
      this.sendToPi = this.sendToPi.bind(this);
      this.clearDrawing = this.clearDrawing.bind(this);
    }
  
    componentDidMount() {
      document.addEventListener("mouseup", this.handleMouseUp);
    }
  
    componentWillUnmount() {
      document.removeEventListener("mouseup", this.handleMouseUp);
    }
  
    handleMouseDown(mouseEvent) {
      if (mouseEvent.button != 0) {
        return;
      }
  
      const point = this.relativeCoordinatesForEvent(mouseEvent);
  
      this.setState(prevState => ({
        lines: prevState.lines.push(new Immutable.List([point])),
        isDrawing: true
      }));
    }
  
    handleMouseMove(mouseEvent) {
      if (!this.state.isDrawing) {
        return;
      }
  
      const point = this.relativeCoordinatesForEvent(mouseEvent);
      
      this.setState(prevState =>  ({
        lines: prevState.lines.updateIn([prevState.lines.size - 1], line => line.push(point))
      }));
    }
  
    handleMouseUp() {
      this.setState({ isDrawing: false });
    }
  
    relativeCoordinatesForEvent(mouseEvent) {
      const boundingRect = this.refs.drawArea.getBoundingClientRect();
      return new Immutable.Map({
        x: mouseEvent.clientX - boundingRect.left,
        y: mouseEvent.clientY - boundingRect.top,
      });
    }

    sendToPi() {
        var stringToSend = "";
        for (var i = 0; i < this.state.lines.size; i++) {
            var line = this.state.lines.get(i);
            for (var j = 0; j < line.size; j++) {
                var point = line.get(j);

                var x = point.get("x");
                var y = point.get("y");

                if (x <= 0 || x > 400 || y <= 0 || y > 400) {
                    continue;
                }

                if ((i + j) % 4 != 0) {
                    continue;
                }

                var yPiCoords = -1 * (x - 200) / 4;
                var zPiCoords = 10 + (400 - y) / 4;

                stringToSend += yPiCoords + "," + zPiCoords + ';';
            }
        }

        stringToSend = stringToSend.substring(0, stringToSend.length - 1);
        console.log(stringToSend);
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ coords: stringToSend })
        };
        fetch('http://localhost:5000/to_pi', requestOptions);
    }

    clearDrawing() {
        this.setState(prevState => ({
            lines: new Immutable.List()
        }));
    }
  
    render() {
      return (
        <div
          className="drawArea"
          ref="drawArea"
          onMouseDown={this.handleMouseDown}
          onMouseMove={this.handleMouseMove}
        >
          <Drawing lines={this.state.lines} />
          <button onClick={this.sendToPi}>
            Send To Pi
          </button>
          <button onClick={this.clearDrawing}>
              Clear Drawing
          </button>
        </div>
      );
    }
  }
  export default DrawArea;
  
  function Drawing({ lines }) {
    return (
      <svg className="drawing">
        {lines.map((line, index) => (
          <DrawingLine key={index} line={line} />
        ))}
      </svg>
    );
  }
  
  function DrawingLine({ line }) {
    const pathData = "M " +
      line
        .map(p => {
          return `${p.get('x')} ${p.get('y')}`;
        })
        .join(" L ");
  
    return <path className="path" d={pathData} />;
  }


import React from 'react';
import Form from 'react';

var TrendGraph = React.createClass({

    getInitialState: function() {
        return {
            graph: "",
            interval: "7 days",
            resolution: "1 days",
            threshold: "50"

        }
    },

    componentDidMount: function() {
        var url = "/api/projects/" + this.props.project_id + "/canary/" + this.props.canary_id +
                  "/trend?interval=" + this.state.interval +
                  "&resolution=" + this.state.resolution +
                  "&threshold=" + this.state.threshold;
        this.canaryRequest = $.get(url, function(result) {
            this.setState({
                graph: result
            })
        }.bind(this))
    },

    componentWillUnmount: function() {
        this.canaryRequest.abort();
    },

    createGraph: function() {
        return {__html: this.state.graph};
    },

    updateGraph: function() {
        var url = "/api/projects/" + this.props.project_id + "/canary/" + this.props.canary_id +
                          "/trend?interval=" + this.state.interval +
                          "&resolution=" + this.state.resolution +
                          "&threshold=" + this.state.threshold;
        this.canaryRequest = $.get(url, function(result) {
                    this.setState({
                        graph: result
                    })
        }.bind(this))
    },

    intervalChange: function(event) {
        this.setState({interval: event.target.value});
    },

    resolutionChange: function(event) {
        this.setState({resolution: event.target.value});
    },

    thresholdChange: function(event) {
        this.setState({threshold: event.target.value});
    },


    render: function() {
        return (
        <div>
             <div>
                <h3>Results Trend Graph</h3>
                <h4>Trend Graph Options</h4>
                  <div className="form-group">
                      <label className="rs-control-label">Interval</label>
                      <input
                        type="text"
                        value={this.state.interval}
                        onChange={this.intervalChange}
                      />
                  </div>
                  <div className="form-group">
                      <label className="rs-control-label">Resolution</label>
                      <input
                        type="text"
                        value={this.state.resolution}
                        onChange={this.resolutionChange}
                      />
                  </div>
                  <div className="form-group">
                      <label className="rs-control-label">Threshold</label>
                      <input
                        type="number"
                        value={this.state.threshold}
                        onChange={this.thresholdChange}
                      />
                  </div>
                  <button className="rs-btn rs-btn-primary" type="button" onClick={this.updateGraph} >Submit</button>
             </div>
              <div dangerouslySetInnerHTML={ this.createGraph() } />
          </div>
        );
    },

});

export default TrendGraph;

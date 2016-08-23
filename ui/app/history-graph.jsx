import React from 'react';

var HealthHistoryGraph = React.createClass({

    getInitialState: function() {
        return {
            graph: ""
        }
    },

    componentDidMount: function() {
        var url = "/api/projects/" + this.props.project_id + "/canary/" + this.props.canary_id +
                  "/history"
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

    render: function() {
        return (
        <div>
              <h3>Canary Health History</h3>
              <div dangerouslySetInnerHTML={ this.createGraph() } />
          </div>
        );
    },

});

export default HealthHistoryGraph;

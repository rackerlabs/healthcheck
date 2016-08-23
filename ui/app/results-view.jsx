import React from 'react';
import ResultsTable from './results-table';
import TrendGraph from './trend-graph';
import HealthHistoryGraph from './history-graph';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';

var ResultsView = React.createClass({

    getInitialState: function() {
        return {
            results: [],
            metadata: {},
        }
    },

    projectId: function() {
        return this.props.params.project_id || this.props.project_id;
    },

    canaryId: function() {
        return this.props.params.canary_id || this.props.canary_id;
    },

    componentDidMount: function() {
        var url = "/api/projects/" + this.projectId() + "/canary/" + this.canaryId() +
                  "/results";
        this.canaryRequest = $.get(url, function(result) {
            this.setState({
                results: result.results
            })
        }.bind(this))
    },

    componentWillUnmount: function() {
        this.canaryRequest.abort();
    },

    render: function() {
        return (
            <div>
                <h2 className="rs-page-title">Canary Results</h2>
                <Tabs>
                  <TabList>
                    <Tab>Canary Health History</Tab>
                    <Tab>Results Trends</Tab>
                  </TabList>

                  <TabPanel>
                  <HealthHistoryGraph project_id={this.projectId()} canary_id={this.canaryId()}/>

                  </TabPanel>

                  <TabPanel>
                  <TrendGraph project_id={this.projectId()} canary_id={this.canaryId()}/>
                  </TabPanel>
                </Tabs>
                <h3>Results</h3>
                <ResultsTable results={this.state.results} />
            </div>
        );
    },

});

export default ResultsView;

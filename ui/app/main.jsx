import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, browserHistory } from 'react-router';
import ProjectsView from './projects-view';
import CanaryView from './canary-view';
import ResultsView from './results-view';

(function() {
    ReactDOM.render(
        <Router history={browserHistory}>
            <Route path="/" component={ProjectsView} />
            <Route path="/projects/:project_id/canary" component={CanaryView} />
            <Route path="/projects/:project_id/canary/:canary_id/results" component={ResultsView} />
        </Router>,
        document.getElementById('content')
    );
})();

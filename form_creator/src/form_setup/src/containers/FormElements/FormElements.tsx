import React, { Component } from "react";
import { connect } from "react-redux";
import { ConnectState } from "../../interfaces";

class FormElements extends Component {
  render() {
    return (
      <div>
        <h1>Form Elements</h1>
        
      </div>
    );
  }
}

const mapStateToProps = (state: ConnectState) => {
  return {
    formElements: state.formSetup.formElements,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(FormElements);

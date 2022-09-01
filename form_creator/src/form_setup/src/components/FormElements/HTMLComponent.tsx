import React, { ChangeEvent } from "react";
import ElementBase, { State } from "./ElementBase";
import Form from "react-bootstrap/Form";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import { HTML_COMPONENT } from "../../elementTypes";
import { APIHTMLComponent, ConnectState } from "../../interfaces";
import { connect } from "react-redux";

class HTMLComponentElem extends ElementBase {
  state = {
    id: null,
    element: {
      html: "",
    },
    elementType: HTML_COMPONENT,
    formChangedSinceSubmit: false,
  };

  onChangeHandler = (_: ChangeEvent, editor: { getData: () => any }) => {
    const data = editor.getData();
    this.setState((prevState: Readonly<State>) => ({
      ...prevState,
      element: {
        ...prevState.element,
        html: data,
      },
      formChangedSinceSubmit: true,
    }));
  };

  isComplete = (): boolean => {
    return Boolean(this.state.element.html);
  };

  

  render() {
    return (
      <this.ElementWrapper>
        <Form.Group controlId="htmlComponent">
          <Form.Label>HTML Component</Form.Label>
          <CKEditor
            editor={ClassicEditor}
            data={this.state.element.html}
            onChange={this.onChangeHandler}
          />
        </Form.Group>
      </this.ElementWrapper>
    );
  }
}

const mapStateToProps = (state: ConnectState) => {
  return {
    httpMethod: state.formSetup.httpMethod,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(HTMLComponentElem);

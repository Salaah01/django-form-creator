import React, { ChangeEvent } from "react";
import ElementBase, { State } from "./ElementBase";
import Form from "react-bootstrap/Form";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import { HTML_COMPONENT } from "../../elementTypes";
import { ConnectState } from "../../interfaces";
import { connect } from "react-redux";
import getAPIEndpoint from "../../apiEndpoints";
import { HTMLComponentFromAPI } from "../../adapters";

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

  elementFromAPI = HTMLComponentFromAPI;

  putURL = (): string => {
    return getAPIEndpoint(
      "form-element-html-component",
      "form-element-html-component-url",
      this.state.id
    );
  };

  render() {
    return (
      <this.ElementWrapper>
        <Form.Group controlId="htmlComponent">
          <Form.Label>HTML Component</Form.Label>
          <CKEditor
            editor={ClassicEditor}
            data={this.state.element.html}
            onReady={(editor: { setData: (arg0: string) => void }) => {
              editor.setData(this.state.element.html);
            }}
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

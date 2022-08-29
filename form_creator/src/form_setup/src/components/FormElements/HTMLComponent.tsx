import React, { ChangeEvent } from "react";
import ElementBase from "./ElementBase";
import Form from "react-bootstrap/Form";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import { HTML_COMPONENT } from "../../elementTypes";

class HTMLComponentElem extends ElementBase {
  state = {
    id: null,
    element: {
      html: "",
    },
    elementType: HTML_COMPONENT,
  };

  onChangeHandler = (_: ChangeEvent, editor: { getData: () => any }) => {
    const data = editor.getData();
    this.setState({ element: { html: data } });
  };

  render() {
    return (
      <this.ElementWrapper>
        <Form.Group controlId="htmlComponent">
          <Form.Label>HTM L Component</Form.Label>
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

export default HTMLComponentElem;

import React, { Component } from "react";
import { HTMLComponent } from "../../interfaces";
import Form from "react-bootstrap/Form";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

interface Props extends HTMLComponent {
  key?: any;
  onUpdateHTML: (html: string) => void;
  [attr: string]: any;
}

class HTMLComponentElem extends Component<any> {
  state = {
    id: null,
    html: ""
  }

  componentDidMount() {
    this.setState({
      id: this.props.id,
      html: this.props.html
    })
  }


  onChangeHandler = (event: any, editor: { getData: () => any }) => {
    const data = editor.getData();
    this.setState({ html: data })
  }

  render() {
    return (<div>
      <Form.Group controlId="htmlComponent">
        <Form.Label>HTML Component</Form.Label>
        <CKEditor
          editor={ClassicEditor}
          data={this.state.html}
          onChange={this.onChangeHandler}
        />
      </Form.Group>
    </div>)
  }
}

export default HTMLComponentElem;

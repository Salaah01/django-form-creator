import * as utils from "./utils";


describe("arrayToObject", () => {
  it("should convert the array to an object.", () => {
    const result = utils.arrayToObject(
      [
        { id: 1, name: "name1", price: 100 },
        { id: 2, name: "name2", price: 200 },
      ],
      "id"
    );
    expect(result).toEqual({
      1: { id: 1, name: "name1", price: 100 },
      2: { id: 2, name: "name2", price: 200 },
    });
  });
});


describe("updateObject", () => {
  let currentObject = { a: 1, b: 2 };

  it("should not mutate the current object but create new object.", () => {
    const newObject = utils.updateObject(currentObject, { a: 2 });
    expect(currentObject).toEqual({ a: 1, b: 2 });
    expect(newObject).toEqual({ a: 2, b: 2 });
  });
});
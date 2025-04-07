/**
 * Request mapper
 */
export class RequestMapper<T> {
  _propertyMapping: any;
  _typeList: any;
  _target: any;

  constructor(type: { new (): T }) {
    this._target = new type();
    this._propertyMapping = this._target.constructor._propertyMap;
    this._typeList = this._target.constructor._typeList;
  }

  map(source: any): any {
    if (!this._propertyMapping) {
      throw new Error('No properties have been mapped.');
    }

    const requestBody: any = {};
    for (const propertyKey in this._propertyMapping) {
      if (source.hasOwnProperty(propertyKey)) {
        const snakeCaseKey = this._propertyMapping[propertyKey];
        let value = source[propertyKey];

        if (typeof value === 'object' && value !== null) {
          if (Array.isArray(value)) {
            if (this._typeList && this._typeList[propertyKey]) {
              value = value.map((item) =>
                new RequestMapper(this._typeList[propertyKey]).map(item)
              );
            }
          } else {
            if (this._typeList && this._typeList[propertyKey]) {
              value = new RequestMapper(this._typeList[propertyKey]).map(value);
            }
          }
        }

        requestBody[snakeCaseKey] = value;
      }
    }
    return requestBody;
  }
}

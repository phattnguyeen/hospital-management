import { propertyMapper } from '../mapper';

export class BOBase {
  @propertyMapper('name', String)
  name: string = '';
}

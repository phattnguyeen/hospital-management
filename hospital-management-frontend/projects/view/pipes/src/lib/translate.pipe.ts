import { Pipe} from '@angular/core';

@Pipe({
  name: 'translate',
  pure: false // Để pipe cập nhật khi thay đổi ngôn ngữ
})
export class TranslatePipe  {

}
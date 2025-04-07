import { Dialog, DialogRef } from '@angular/cdk/dialog';
import { DOCUMENT } from '@angular/common';
import { inject, Renderer2, Type } from '@angular/core';
import { Router } from '@angular/router';
import { BROWSER_STORAGE } from '@infrastructure/base';
import { VIEW_CONTEXT } from './view.aggregation.context';
import { ViewOptions } from './view.option';
import { ActionHandlerType } from './view.type';

export abstract class ViewComponnet {
  protected readonly _router = inject(Router);
  protected readonly _renderer = inject(Renderer2);
  protected readonly _dialog = inject(Dialog);
  protected readonly _document = inject(DOCUMENT);
  protected readonly _storage = inject(BROWSER_STORAGE);
  protected readonly _context = inject(VIEW_CONTEXT);

  /**
   * Open dialog with options
   * @param {DialogOptions} options
   * @param {Type<T>} componentType
   */
  public openDialog<T extends ViewOptions>(componentType: Type<T>, options?: T) {
    const dialogConfig = {
      data: options,
      disableClose: options?.disableClose ?? true,
      autoFocus: true,
      hasBackdrop: true,
      restoreFocus: true,
      width: options ? undefined : '530px',
    };

    let dialogRef: DialogRef<unknown, T> | DialogRef<unknown> | null = null;

    if (componentType) {
      dialogRef = this._dialog.open(componentType, dialogConfig);
      dialogRef.closed.subscribe((result) => {
        if (options?.actionHandler) {
          const actionResult = result as ActionHandlerType;
          options.actionHandler(actionResult);
        }
      });
    }
  }
}

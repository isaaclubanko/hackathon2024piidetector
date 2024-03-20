export class PIIResponseModel {
  word: string;
  entityGroup: string;

  constructor(data:any) {
    this.word = data.word;
    this.entityGroup = data.entityGroup;
  }
}

export class PIIResponseAdapter {
  adapt(item: any): PIIResponseModel {
    return new PIIResponseModel({
      word: item.word,
      entityGroup: item.entity_group
    });
  }
}
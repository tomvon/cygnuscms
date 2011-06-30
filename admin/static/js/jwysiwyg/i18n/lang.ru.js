/**
 * Internationalization: russian language
 * 
 * Depends on jWYSIWYG, $.wysiwyg.i18n
 */
(function($) {
if (undefined === $.wysiwyg) {
	throw "lang.ru.js depends on $.wysiwyg";
	return false;
}
if (undefined === $.wysiwyg.i18n) {
	throw "lang.ru.js depends on $.wysiwyg.i18n";
	return false;
}

$.wysiwyg.i18n.lang.ru = {
"Bold": "Жирный",
"Copy": "Копировать",
"Create link": "Создать ссылку",
"Cut": "Вырезать",
"Decrease font size": "Уменьшить шрифт",
"Header 1": "Заголовок 1",
"Header 2": "Заголовок 2",
"Header 3": "Заголовок 3",
"View source code": "Посмотреть исходный код",
"Increase font size": "Увеличить шрифт",
"Indent": "Отступ",
"Insert Horizontal Rule": "Вставить горизонтальную прямую",
"Insert image": "Вставить изображение",
"Insert Ordered List": "Вставить нумерованный список",
"Insert table": "Вставить таблицу",
"Insert Unordered List": "Вставить ненумерованный список",
"Italic": "Курсив",
"Justify Center": "Выровнять по центру",
"Justify Full": "Выровнять по ширине",
"Justify Left": "Выровнять по левой стороне",
"Justify Right": "Выровнять по правой стороне",
"Left to Right": "Слева направо",
"Outdent": "Убрать отступ",
"Paste": "Вставить",
"Redo": "Вернуть действие",
"Remove formatting": "Убрать форматирование",
"Right to Left": "Справа налево",
"Strike-through": "Зачёркнутый",
"Subscript": "Нижний регистр",
"Superscript": "Верхний регистр",
"Underline": "Подчёркнутый",
"Undo": "Отменить действие"
};

})(jQuery);
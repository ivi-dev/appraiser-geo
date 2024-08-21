$CsvOut = Get-Content '.\resources\Градове-Форматирани`[CSV`].json'
$TextOut = Get-Content '.\resources\Градове-Форматирани`[TEXT`].json'

Compare-Object $CsvOut $TextOut
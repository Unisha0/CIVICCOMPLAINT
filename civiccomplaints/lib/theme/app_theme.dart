import 'package:flutter/material.dart';

const primaryColor = Color(0xff082659);
const secondaryColor = Color(0xff51eec2);

final appTheme = ThemeData(
  brightness: Brightness.light,
  primaryColor: primaryColor,

  appBarTheme: const AppBarTheme(
    backgroundColor: primaryColor,
    centerTitle: true,
  ),

  colorScheme: ColorScheme.fromSeed(
    seedColor: primaryColor,
    primary: primaryColor,
    secondary: secondaryColor,
  ),

  cardTheme: const CardThemeData(
    elevation: 4,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.all(Radius.circular(12)),
    ),
  ),
);
from enum import StrEnum

from settings import (GPT, GPT_ALIAS, HOBBY, LOVE_STORY, SCHOOL_PHOTO, SELFIE,
                      SQL_ALIAS, SQL_NOSQL)


class Question(StrEnum):
    GPT = GPT.lower()
    HOBBY = HOBBY.lower()
    LOVE_STORY = LOVE_STORY.lower()
    SCHOOL_PHOTO = SCHOOL_PHOTO.lower()
    SELFIE = SELFIE.lower()
    SQL_NOSQL = SQL_NOSQL.lower()

    GPT_ALIAS = GPT_ALIAS
    SQL_ALIAS = SQL_ALIAS

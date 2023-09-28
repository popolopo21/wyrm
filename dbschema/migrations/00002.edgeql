CREATE MIGRATION m1xl5wouhaitchjbzmubwir4wgmajdb22fl6js46ozrfdrzfzl2sdq
    ONTO m1gascfy4xfhm2vbuphjd4swr2b3swcfi2qxs2mmxa4f4tyfzuyqcq
{
  ALTER TYPE default::Article {
      CREATE PROPERTY tags: array<std::str>;
  };
};

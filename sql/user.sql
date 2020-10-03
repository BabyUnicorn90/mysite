desc user;

-- 조회
Select * from user;



-- 회원가입
insert
	into user
values (null, '둘리', 'dooly@gamil.com',  password('1234'), 'male', now());

-- login
select * 
	from user
where email='dooly@gamil.com' 
	and password=password('1234');


-- 회원정보수정
update

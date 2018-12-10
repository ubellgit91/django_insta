# MTV 패턴

Django는 Model, Template, View라는 MTV 패턴을 따르고 있는데, MTV은 MVC (Model View Controller)와 유사한 점이 많다. Django는 Controller의 역활을 Django Framework 자체에서 한다고 보고 있으며, 따라서 MVC와 약간 다른 미묘한 차이를 MTV로 설명하고 있다.

MTV에서의 Model은 데이타를 표현하는데 사용되며, 하나의 모델 클래스는 DB에서 하나의 테이블로 표현된다. MTV의 View는 HTTP Request를 받아 그 결과인 HTTP Response를 리턴하는 컴포넌트로서, Model로부터 데이타를 읽거나 저장할 수 있으며, Template을 호출하여 데이타를 UI 상에 표현하도록 할 수 있다. MTV의 Template은 Presentation Logic 만을 갖는데 HTML을 생성하는 것을 목적으로 하는 컴포넌트이다.
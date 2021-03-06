# 재무모델(Financial cashflow model) 작성을 위한 모듈

### PrjtCF_module
"PrjtCF_module"은
각종 사업 검토시 재무적인 측면에서 사업의 현금흐름을 추정하는데 적용 가능한 모듈입니다.

Index, Account와 Loan 모듈을 사용하면 재무기획자 입장에서 검토 중인 사업의 현금흐름을 좀 더 용이하게 추정할 수 있습니다.

재무기획자, 프로젝트 성 투자를 담당하는 투자자 등은 수시로 기획사업 및 투자대상 등에 대하여 현금흐름을 추정하면서 투자 적정성을 검토합니다.
저는 주로 부동산 개발사업 및 부동산 투자를 업으로 하고 있으므로, 부동산 개발사업 중심으로 예시를 작성하였습니다.
하지만, 다른 인프라 사업, 신규 추진 사업 등 각종 재무모델이 필요한 곳에 사용 가능할 것으로 생각됩니다.

엑셀로 재무모델을 작성하는데에는 최소 수일 내지 수주의 시간이 소요되곤 하며,
이 또한 개별 사업 및 투자건에 맞춰 모델을 수정하거나, 신규 작성하는데에도 그와 유사한 시간이 소요됩니다.
모델의 규모가 일정 수준 이상 커지면 이를 해석하는 것도, 수정하는 것도 보통 일이 아닙니다.

엑셀을 붙잡고 있는 시간과 노력을 크게 줄여보고자 모듈 작성을 시작하였습니다.

### Example
2021년 7월 작성한 간단한 CashFlow 샘플 부터 시작하여 계속 적용 사례를 확대하고 있습니다.
현재는 개발 후 운영을 계획하는 부동산 개발사업에 대하여 적용 중이며, 향후 분양 사업 등에 대해서 적용 사례를 확장하고자 합니다.
지속적으로 Example에 적용하면서 모듈에 대한 완성도를 높여가는 작업 중입니다.

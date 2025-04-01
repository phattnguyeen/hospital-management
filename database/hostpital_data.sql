CREATE TABLE public.account (
    account_id uuid DEFAULT gen_random_uuid() NOT NULL,
    username character varying(50) NOT NULL,
    "passwordHash" text NOT NULL,
    role character varying(20) NOT NULL,
    patient_id character varying(20),
    doctor_id character varying(20),
    employee_id character varying(20)
);



--
--

CREATE TABLE public.appointment (
    appointment_id character varying(20) NOT NULL,
    patient_id character varying(20) NOT NULL,
    doctor_id character varying(20) NOT NULL,
    request_date date NOT NULL,
    appointment_time time without time zone,
    status character varying(50),
    appointment_date date NOT NULL
);



--
--

CREATE TABLE public.department (
    department_id character varying(20) NOT NULL,
    department_name character varying(100) NOT NULL
);



--
--

CREATE TABLE public.disease (
    disease_id uuid DEFAULT gen_random_uuid() NOT NULL,
    disease_name character varying(100) NOT NULL
);



--
--

CREATE TABLE public.doctor (
    doctor_id character varying(20) NOT NULL,
    full_name character varying(100) NOT NULL,
    birth_date date,
    gender character varying(10),
    address character varying(255),
    phone_number character varying(20),
    national_id character varying(20),
    experience integer,
    department_id character varying(20),
    CONSTRAINT doctor_experience_check CHECK ((experience >= 0)),
    CONSTRAINT doctor_gender_check CHECK (((gender)::text = ANY ((ARRAY['Male'::character varying, 'Female'::character varying, 'Other'::character varying])::text[])))
);



--
--

CREATE TABLE public.employee (
    employee_id character varying(20) NOT NULL,
    full_name character varying(100) NOT NULL,
    birth_date date,
    gender character varying(10),
    address character varying(255),
    phone_number character varying(20),
    "position" character varying(50) NOT NULL,
    department_id character varying(20),
    CONSTRAINT employee_gender_check CHECK (((gender)::text = ANY ((ARRAY['Male'::character varying, 'Female'::character varying, 'Other'::character varying])::text[])))
);



--
--

CREATE TABLE public.insurance (
    insurance_id character varying(20) NOT NULL,
    patient_id character varying(20) NOT NULL,
    treatment_facility character varying(255)
);



--
--

CREATE TABLE public.invoice (
    invoice_id character varying(20) NOT NULL,
    total_amount numeric(15,2),
    expense numeric(15,2),
    payment_date date,
    status character varying(50),
    employee_id character varying(20),
    CONSTRAINT invoice_expense_check CHECK ((expense >= (0)::numeric)),
    CONSTRAINT invoice_total_amount_check CHECK ((total_amount >= (0)::numeric))
);



--
--

CREATE TABLE public.medical_examination (
    exam_id character varying(20) NOT NULL,
    patient_id character varying(20) NOT NULL,
    doctor_id character varying(20) NOT NULL,
    exam_date date NOT NULL,
    symptoms text,
    disease_id uuid
);



--
--

CREATE TABLE public.medical_record (
    record_id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id character varying(20) NOT NULL,
    doctor_id character varying(20) NOT NULL,
    exam_date date NOT NULL,
    symptoms text,
    diagnosis text,
    treatment text,
    department_id character varying(20)
);



--
--

CREATE TABLE public.medicine (
    medicine_id character varying(20) NOT NULL,
    medicine_name character varying(100) NOT NULL,
    category character varying(50),
    unit character varying(20),
    price numeric(10,2),
    expiration_date date,
    notes text,
    CONSTRAINT medicine_price_check CHECK ((price >= (0)::numeric))
);



--
--

CREATE TABLE public.patient (
    patient_id character varying(20) NOT NULL,
    full_name character varying(100) NOT NULL,
    birth_date date,
    gender character varying(10),
    address character varying(255),
    phone_number character varying(20),
    medical_history text,
    CONSTRAINT patient_gender_check CHECK (((gender)::text = ANY ((ARRAY['Male'::character varying, 'Female'::character varying, 'Other'::character varying])::text[])))
);



--
--

CREATE TABLE public.prescription (
    medicine_id character varying(20) NOT NULL,
    doctor_id character varying(20) NOT NULL,
    patient_id character varying(20) NOT NULL,
    invoice_id character varying(20),
    quantity integer,
    prescription_date date,
    notes text,
    CONSTRAINT prescription_quantity_check CHECK ((quantity > 0))
);



--
--

CREATE TABLE public.room (
    room_id character varying(20) NOT NULL,
    room_type character varying(50) NOT NULL,
    bed_id character varying(50) NOT NULL,
    status character varying(50),
    department_id character varying(20)
);



--
--

CREATE TABLE public.service (
    service_id uuid DEFAULT gen_random_uuid() NOT NULL,
    service_name character varying(100) NOT NULL,
    unit_price numeric(10,2),
    unit character varying(20),
    CONSTRAINT service_unit_price_check CHECK ((unit_price >= (0)::numeric))
);



--
--

CREATE TABLE public.service_detail (
    service_id uuid NOT NULL,
    patient_id character varying(20) NOT NULL,
    quantity integer,
    usage_date date NOT NULL,
    CONSTRAINT service_detail_quantity_check CHECK ((quantity > 0))
);



--
--

-- COPY public.account (account_id, username, "passwordHash", role, patient_id, doctor_id, employee_id) FROM stdin;



-- --
-- --

-- COPY public.appointment (appointment_id, patient_id, doctor_id, request_date, appointment_time, status, appointment_date) FROM stdin;



-- --
-- --

-- COPY public.department (department_id, department_name) FROM stdin;



-- --
-- --

-- COPY public.disease (disease_id, disease_name) FROM stdin;



-- --
-- --

-- COPY public.doctor (doctor_id, full_name, birth_date, gender, address, phone_number, national_id, experience, department_id) FROM stdin;



-- --
-- --

-- COPY public.employee (employee_id, full_name, birth_date, gender, address, phone_number, "position", department_id) FROM stdin;



-- --
-- --

-- COPY public.insurance (insurance_id, patient_id, treatment_facility) FROM stdin;



-- --
-- --

-- COPY public.invoice (invoice_id, total_amount, expense, payment_date, status, employee_id) FROM stdin;



-- --
-- --

-- COPY public.medical_examination (exam_id, patient_id, doctor_id, exam_date, symptoms, disease_id) FROM stdin;



-- --
-- --

-- COPY public.medical_record (record_id, patient_id, doctor_id, exam_date, symptoms, diagnosis, treatment, department_id) FROM stdin;



-- --
-- --

-- COPY public.medicine (medicine_id, medicine_name, category, unit, price, expiration_date, notes) FROM stdin;



-- --
-- --

-- COPY public.patient (patient_id, full_name, birth_date, gender, address, phone_number, medical_history) FROM stdin;



-- --
-- --

-- COPY public.prescription (medicine_id, doctor_id, patient_id, invoice_id, quantity, prescription_date, notes) FROM stdin;



-- --
-- --

-- COPY public.room (room_id, room_type, bed_id, status, department_id) FROM stdin;



-- --
-- --

-- COPY public.service (service_id, service_name, unit_price, unit) FROM stdin;



-- --
-- --

-- COPY public.service_detail (service_id, patient_id, quantity, usage_date) FROM stdin;



--
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "ACCOUNT_doctor_id_key" UNIQUE (doctor_id);


--
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "ACCOUNT_employee_id_key" UNIQUE (employee_id);


--
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "ACCOUNT_patient_id_key" UNIQUE (patient_id);


--
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "ACCOUNT_pkey" PRIMARY KEY (account_id);


--
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "ACCOUNT_username_key" UNIQUE (username);


--
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);


--
--

ALTER TABLE ONLY public.department
    ADD CONSTRAINT department_pkey PRIMARY KEY (department_id);


--
--

ALTER TABLE ONLY public.disease
    ADD CONSTRAINT disease_pkey PRIMARY KEY (disease_id);


--
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_national_id_key UNIQUE (national_id);


--
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_phone_number_key UNIQUE (phone_number);


--
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_pkey PRIMARY KEY (doctor_id);


--
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_phone_number_key UNIQUE (phone_number);


--
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (employee_id);


--
--

ALTER TABLE ONLY public.insurance
    ADD CONSTRAINT insurance_pkey PRIMARY KEY (insurance_id);


--
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_pkey PRIMARY KEY (invoice_id);


--
--

ALTER TABLE ONLY public.medical_examination
    ADD CONSTRAINT medical_examination_pkey PRIMARY KEY (exam_id);


--
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT medical_record_pkey PRIMARY KEY (record_id);


--
--

ALTER TABLE ONLY public.medicine
    ADD CONSTRAINT medicine_pkey PRIMARY KEY (medicine_id);


--
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_phone_number_key UNIQUE (phone_number);


--
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);


--
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_pkey PRIMARY KEY (medicine_id, doctor_id, patient_id);


--
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (room_id);


--
--

ALTER TABLE ONLY public.service_detail
    ADD CONSTRAINT service_detail_pkey PRIMARY KEY (service_id, patient_id);


--
--

ALTER TABLE ONLY public.service
    ADD CONSTRAINT service_pkey PRIMARY KEY (service_id);


--
--

CREATE INDEX "ix_ACCOUNT_account_id" ON public.account USING btree (account_id);


--
--

CREATE INDEX ix_disease_disease_id ON public.disease USING btree (disease_id);


--
--

CREATE INDEX ix_medical_record_record_id ON public.medical_record USING btree (record_id);


--
--

CREATE INDEX ix_service_service_id ON public.service USING btree (service_id);


--
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "ACCOUNT_doctor_id_fkey" FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id) ON DELETE CASCADE;


--
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "ACCOUNT_employee_id_fkey" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE CASCADE;


--
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "ACCOUNT_patient_id_fkey" FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id) ON DELETE CASCADE;


--
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


--
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


--
--

ALTER TABLE ONLY public.insurance
    ADD CONSTRAINT insurance_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id);


--
--

ALTER TABLE ONLY public.medical_examination
    ADD CONSTRAINT medical_examination_disease_id_fkey FOREIGN KEY (disease_id) REFERENCES public.disease(disease_id);


--
--

ALTER TABLE ONLY public.medical_examination
    ADD CONSTRAINT medical_examination_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
--

ALTER TABLE ONLY public.medical_examination
    ADD CONSTRAINT medical_examination_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT medical_record_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


--
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT medical_record_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT medical_record_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES public.invoice(invoice_id);


--
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_medicine_id_fkey FOREIGN KEY (medicine_id) REFERENCES public.medicine(medicine_id);


--
--

ALTER TABLE ONLY public.prescription
    ADD CONSTRAINT prescription_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


--
--

ALTER TABLE ONLY public.service_detail
    ADD CONSTRAINT service_detail_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id);


--
--

ALTER TABLE ONLY public.service_detail
    ADD CONSTRAINT service_detail_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.service(service_id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--



--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--



--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--



--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--



--
-- PostgreSQL database dump complete
--



-- Suggested Indexes for Optimization
